#include <errno.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    uint64_t state;
    uint64_t inc;
    int has_spare;
    double spare;
} rng_t;

typedef struct {
    int n;
    double dt;
    double burn_time;
    double sample_time;
    int sample_stride;
    double gamma;
    double omega_scale;
    double coupling;
    double diffusion;
    uint64_t seed;
} sim_config_t;

typedef struct {
    double mean_r;
    double sd_r;
    long samples;
} sim_result_t;

static uint32_t pcg32(rng_t *rng) {
    uint64_t oldstate = rng->state;
    uint32_t xorshifted;
    uint32_t rot;

    rng->state = oldstate * 6364136223846793005ULL + rng->inc;
    xorshifted = (uint32_t)(((oldstate >> 18U) ^ oldstate) >> 27U);
    rot = (uint32_t)(oldstate >> 59U);
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

static void rng_seed(rng_t *rng, uint64_t seed, uint64_t stream) {
    rng->state = 0U;
    rng->inc = (stream << 1U) | 1U;
    rng->has_spare = 0;
    (void)pcg32(rng);
    rng->state += seed;
    (void)pcg32(rng);
}

static double uniform_open(rng_t *rng) {
    return ((double)pcg32(rng) + 0.5) / 4294967296.0;
}

static double normal01(rng_t *rng) {
    double u;
    double v;
    double s;
    double factor;

    if (rng->has_spare) {
        rng->has_spare = 0;
        return rng->spare;
    }
    do {
        u = 2.0 * uniform_open(rng) - 1.0;
        v = 2.0 * uniform_open(rng) - 1.0;
        s = u * u + v * v;
    } while (s <= 0.0 || s >= 1.0);
    factor = sqrt(-2.0 * log(s) / s);
    rng->spare = v * factor;
    rng->has_spare = 1;
    return u * factor;
}

static void shuffle(double *values, int n, rng_t *rng) {
    int i;
    for (i = n - 1; i > 0; --i) {
        int j = (int)(uniform_open(rng) * (double)(i + 1));
        double tmp = values[i];
        values[i] = values[j];
        values[j] = tmp;
    }
}

static int run_simulation(const sim_config_t *cfg, sim_result_t *result,
                          double *agent_omega, double *agent_alignment) {
    double *theta = NULL;
    double *omega = NULL;
    double *theta_cos = NULL;
    double *theta_sin = NULL;
    double *alignment_sum = NULL;
    rng_t rng;
    int burn_steps;
    int sample_steps;
    int total_steps;
    int step;
    long samples = 0;
    double r_sum = 0.0;
    double r_sq_sum = 0.0;
    double noise_scale;

    theta = (double *)malloc((size_t)cfg->n * sizeof(double));
    omega = (double *)malloc((size_t)cfg->n * sizeof(double));
    theta_cos = (double *)malloc((size_t)cfg->n * sizeof(double));
    theta_sin = (double *)malloc((size_t)cfg->n * sizeof(double));
    if (agent_alignment != NULL) {
        alignment_sum = (double *)calloc((size_t)cfg->n, sizeof(double));
    }
    if (theta == NULL || omega == NULL || theta_cos == NULL ||
        theta_sin == NULL ||
        (agent_alignment != NULL && alignment_sum == NULL)) {
        fprintf(stderr, "allocation failed for n=%d\n", cfg->n);
        free(theta);
        free(omega);
        free(theta_cos);
        free(theta_sin);
        free(alignment_sum);
        return 1;
    }

    rng_seed(&rng, cfg->seed, 54U);
    for (int i = 0; i < cfg->n; ++i) {
        double p = ((double)i + 0.5) / (double)cfg->n;
        omega[i] = cfg->gamma * tan(M_PI * (p - 0.5));
    }
    shuffle(omega, cfg->n, &rng);
    for (int i = 0; i < cfg->n; ++i) {
        theta[i] = 2.0 * M_PI * uniform_open(&rng);
        if (agent_omega != NULL) {
            agent_omega[i] = cfg->omega_scale * omega[i];
        }
    }

    burn_steps = (int)llround(cfg->burn_time / cfg->dt);
    sample_steps = (int)llround(cfg->sample_time / cfg->dt);
    total_steps = burn_steps + sample_steps;
    noise_scale = sqrt(2.0 * cfg->diffusion * cfg->dt);

    for (step = 0; step < total_steps; ++step) {
        double mean_cos = 0.0;
        double mean_sin = 0.0;
        double r;

        for (int i = 0; i < cfg->n; ++i) {
            theta_cos[i] = cos(theta[i]);
            theta_sin[i] = sin(theta[i]);
            mean_cos += theta_cos[i];
            mean_sin += theta_sin[i];
        }
        mean_cos /= (double)cfg->n;
        mean_sin /= (double)cfg->n;
        r = hypot(mean_cos, mean_sin);

        if (step >= burn_steps &&
            ((step - burn_steps) % cfg->sample_stride) == 0) {
            r_sum += r;
            r_sq_sum += r * r;
            ++samples;
            if (alignment_sum != NULL && r > 1e-14) {
                for (int i = 0; i < cfg->n; ++i) {
                    alignment_sum[i] +=
                        (theta_cos[i] * mean_cos + theta_sin[i] * mean_sin) / r;
                }
            }
        }

        for (int i = 0; i < cfg->n; ++i) {
            double mean_field = cfg->coupling *
                                (mean_sin * theta_cos[i] -
                                 mean_cos * theta_sin[i]);
            theta[i] += (cfg->omega_scale * omega[i] + mean_field) * cfg->dt +
                        noise_scale * normal01(&rng);
        }
    }

    result->samples = samples;
    result->mean_r = r_sum / (double)samples;
    if (samples > 1) {
        double variance =
            (r_sq_sum - r_sum * r_sum / (double)samples) / (double)(samples - 1);
        result->sd_r = sqrt(variance > 0.0 ? variance : 0.0);
    } else {
        result->sd_r = 0.0;
    }
    if (agent_alignment != NULL) {
        for (int i = 0; i < cfg->n; ++i) {
            agent_alignment[i] = alignment_sum[i] / (double)samples;
        }
    }

    free(theta);
    free(omega);
    free(theta_cos);
    free(theta_sin);
    free(alignment_sum);
    return 0;
}

static FILE *open_output(const char *dir, const char *name, char *path,
                         size_t path_size) {
    int written = snprintf(path, path_size, "%s/%s", dir, name);
    FILE *file;
    if (written < 0 || (size_t)written >= path_size) {
        fprintf(stderr, "output path is too long\n");
        return NULL;
    }
    file = fopen(path, "w");
    if (file == NULL) {
        fprintf(stderr, "cannot open %s: %s\n", path, strerror(errno));
    }
    return file;
}

static int run_k_sweep(const char *out_dir) {
    static const double k_values[] = {
        0.30, 0.45, 0.60, 0.68, 0.72, 0.74, 0.76,
        0.80, 0.86, 0.95, 1.10, 1.40, 2.00, 3.45
    };
    static const uint64_t seeds[] = {1729U, 2718U, 31415U};
    char path[4096];
    FILE *file = open_output(out_dir, "T1_k_sweep.csv", path, sizeof(path));
    if (file == NULL) {
        return 1;
    }
    fprintf(file,
            "K,gamma,D,Kc,N,dt,burn_time,sample_time,sample_stride,seed,mean_r,sd_r,samples\n");
    for (size_t k_index = 0; k_index < sizeof(k_values) / sizeof(k_values[0]);
         ++k_index) {
        for (size_t seed_index = 0; seed_index < sizeof(seeds) / sizeof(seeds[0]);
             ++seed_index) {
            sim_config_t cfg = {
                .n = 512,
                .dt = 0.01,
                .burn_time = 240.0,
                .sample_time = 160.0,
                .sample_stride = 5,
                .gamma = 0.25,
                .omega_scale = 1.0,
                .coupling = k_values[k_index],
                .diffusion = 0.12,
                .seed = seeds[seed_index],
            };
            sim_result_t result;
            if (run_simulation(&cfg, &result, NULL, NULL) != 0) {
                fclose(file);
                return 1;
            }
            fprintf(file,
                    "%.17g,%.17g,%.17g,%.17g,%d,%.17g,%.17g,%.17g,%d,%llu,%.17g,%.17g,%ld\n",
                    cfg.coupling, cfg.gamma, cfg.diffusion,
                    2.0 * (cfg.gamma + cfg.diffusion), cfg.n, cfg.dt,
                    cfg.burn_time, cfg.sample_time, cfg.sample_stride,
                    (unsigned long long)cfg.seed, result.mean_r, result.sd_r,
                    result.samples);
            fflush(file);
        }
    }
    fclose(file);
    return 0;
}

static int run_c06_policies(const char *out_dir) {
    static const uint64_t seeds[] = {1729U, 2718U, 31415U};
    static const char *names[] = {
        "no_change", "pure_generator_slowdown", "frequency_narrowing_only"
    };
    static const double omega_scales[] = {1.0, 0.5, 0.5};
    static const double k_values[] = {0.60, 0.30, 0.60};
    static const double d_values[] = {0.12, 0.06, 0.12};
    static const double time_scales[] = {1.0, 2.0, 1.0};
    static const double dt_values[] = {0.01, 0.02, 0.01};
    char path[4096];
    FILE *file =
        open_output(out_dir, "T1_c06_policies.csv", path, sizeof(path));
    if (file == NULL) {
        return 1;
    }
    fprintf(file,
            "policy,omega_scale,K,D,effective_gamma,Kc,K_over_Kc,N,dt,burn_time,sample_time,seed,mean_r,sd_r,samples\n");
    for (size_t policy = 0; policy < sizeof(names) / sizeof(names[0]); ++policy) {
        for (size_t seed_index = 0; seed_index < sizeof(seeds) / sizeof(seeds[0]);
             ++seed_index) {
            double effective_gamma = 0.25 * omega_scales[policy];
            double kc = 2.0 * (effective_gamma + d_values[policy]);
            sim_config_t cfg = {
                .n = 512,
                .dt = dt_values[policy],
                .burn_time = 240.0 * time_scales[policy],
                .sample_time = 160.0 * time_scales[policy],
                .sample_stride = 5,
                .gamma = 0.25,
                .omega_scale = omega_scales[policy],
                .coupling = k_values[policy],
                .diffusion = d_values[policy],
                .seed = seeds[seed_index],
            };
            sim_result_t result;
            if (run_simulation(&cfg, &result, NULL, NULL) != 0) {
                fclose(file);
                return 1;
            }
            fprintf(file,
                    "%s,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%d,%.17g,%.17g,%.17g,%llu,%.17g,%.17g,%ld\n",
                    names[policy], cfg.omega_scale, cfg.coupling, cfg.diffusion,
                    effective_gamma, kc, cfg.coupling / kc, cfg.n, cfg.dt,
                    cfg.burn_time, cfg.sample_time,
                    (unsigned long long)cfg.seed, result.mean_r, result.sd_r,
                    result.samples);
            fflush(file);
        }
    }
    fclose(file);
    return 0;
}

static int run_convergence(const char *out_dir) {
    static const double k_values[] = {0.60, 0.80, 3.45};
    static const double dt_values[] = {0.04, 0.02, 0.01, 0.005};
    static const int n_values[] = {256, 512, 1024};
    static const uint64_t seeds[] = {1729U, 2718U, 31415U};
    char path[4096];
    FILE *file =
        open_output(out_dir, "T1_convergence.csv", path, sizeof(path));
    if (file == NULL) {
        return 1;
    }
    fprintf(file,
            "axis,axis_value,K,N,dt,burn_time,sample_time,seed,mean_r,sd_r,samples\n");
    for (size_t k_index = 0; k_index < sizeof(k_values) / sizeof(k_values[0]);
         ++k_index) {
        for (size_t dt_index = 0; dt_index < sizeof(dt_values) / sizeof(dt_values[0]);
             ++dt_index) {
            for (size_t seed_index = 0;
                 seed_index < sizeof(seeds) / sizeof(seeds[0]); ++seed_index) {
                sim_config_t cfg = {
                    .n = 512,
                    .dt = dt_values[dt_index],
                    .burn_time = 240.0,
                    .sample_time = 160.0,
                    .sample_stride = 5,
                    .gamma = 0.25,
                    .omega_scale = 1.0,
                    .coupling = k_values[k_index],
                    .diffusion = 0.12,
                    .seed = seeds[seed_index],
                };
                sim_result_t result;
                if (run_simulation(&cfg, &result, NULL, NULL) != 0) {
                    fclose(file);
                    return 1;
                }
                fprintf(file,
                        "dt,%.17g,%.17g,%d,%.17g,%.17g,%.17g,%llu,%.17g,%.17g,%ld\n",
                        cfg.dt, cfg.coupling, cfg.n, cfg.dt, cfg.burn_time,
                        cfg.sample_time, (unsigned long long)cfg.seed,
                        result.mean_r, result.sd_r, result.samples);
            }
        }
        for (size_t n_index = 0; n_index < sizeof(n_values) / sizeof(n_values[0]);
             ++n_index) {
            for (size_t seed_index = 0;
                 seed_index < sizeof(seeds) / sizeof(seeds[0]); ++seed_index) {
                sim_config_t cfg = {
                    .n = n_values[n_index],
                    .dt = 0.01,
                    .burn_time = 240.0,
                    .sample_time = 160.0,
                    .sample_stride = 5,
                    .gamma = 0.25,
                    .omega_scale = 1.0,
                    .coupling = k_values[k_index],
                    .diffusion = 0.12,
                    .seed = seeds[seed_index],
                };
                sim_result_t result;
                if (run_simulation(&cfg, &result, NULL, NULL) != 0) {
                    fclose(file);
                    return 1;
                }
                fprintf(file,
                        "N,%d,%.17g,%d,%.17g,%.17g,%.17g,%llu,%.17g,%.17g,%ld\n",
                        cfg.n, cfg.coupling, cfg.n, cfg.dt, cfg.burn_time,
                        cfg.sample_time, (unsigned long long)cfg.seed,
                        result.mean_r, result.sd_r, result.samples);
            }
        }
        fflush(file);
    }
    fclose(file);
    return 0;
}

static int run_c07_outcomes(const char *out_dir) {
    char path[4096];
    FILE *file =
        open_output(out_dir, "T1_c07_agent_outcomes.csv", path, sizeof(path));
    double *omega;
    double *alignment;
    sim_config_t cfg = {
        .n = 1024,
        .dt = 0.01,
        .burn_time = 240.0,
        .sample_time = 160.0,
        .sample_stride = 5,
        .gamma = 0.25,
        .omega_scale = 1.0,
        .coupling = 1.10,
        .diffusion = 0.12,
        .seed = 424242U,
    };
    sim_result_t result;
    if (file == NULL) {
        return 1;
    }
    omega = (double *)malloc((size_t)cfg.n * sizeof(double));
    alignment = (double *)malloc((size_t)cfg.n * sizeof(double));
    if (omega == NULL || alignment == NULL) {
        fprintf(stderr, "allocation failed for C07 output\n");
        free(omega);
        free(alignment);
        fclose(file);
        return 1;
    }
    if (run_simulation(&cfg, &result, omega, alignment) != 0) {
        free(omega);
        free(alignment);
        fclose(file);
        return 1;
    }
    fprintf(file,
            "agent_id,seed,K,gamma,D,global_mean_r,intrinsic_omega,abs_intrinsic_omega,mean_local_alignment\n");
    for (int i = 0; i < cfg.n; ++i) {
        fprintf(file, "%d,%llu,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g\n",
                i, (unsigned long long)cfg.seed, cfg.coupling, cfg.gamma,
                cfg.diffusion, result.mean_r, omega[i], fabs(omega[i]),
                alignment[i]);
    }
    free(omega);
    free(alignment);
    fclose(file);
    return 0;
}

int main(int argc, char **argv) {
    const char *out_dir;
    if (argc != 2) {
        fprintf(stderr, "usage: %s RAW_OUTPUT_DIR\n", argv[0]);
        return 2;
    }
    out_dir = argv[1];
    if (run_k_sweep(out_dir) != 0) {
        return 1;
    }
    if (run_c06_policies(out_dir) != 0) {
        return 1;
    }
    if (run_convergence(out_dir) != 0) {
        return 1;
    }
    if (run_c07_outcomes(out_dir) != 0) {
        return 1;
    }
    return 0;
}
