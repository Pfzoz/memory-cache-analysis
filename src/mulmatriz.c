#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_matrix(double **matrix, int m, int n)
{
    for (int i = 0; i < m; i++)
    {
        for (int ia = 0; ia < n; ia++)
        {
            printf("[%f] ", matrix[i][ia]);
        }
        printf("\n");
    }
    printf("\n");
}

double **create_r_matrix(int m, int n)
{
    double **result = malloc(m*sizeof(double*));
    for (int i = 0; i < m; i++)
    {
        result[i] = malloc(n*sizeof(double));
    }

    for (int i = 0; i < m; i++)
    {
        for (int ia = 0; ia < n; ia++)
        {
            double range = (RAND_MAX-0); 
            double div = RAND_MAX / range;
            result[i][ia] = 0 + (rand() / div);
        }
    }

    return result;
}

double **norm_multiply(double **a, double **b, int m, int n, int bm, int bn)
{
    if (n != bm)
    {
        printf("Invalid matrix parameters.\n");
        exit(0);
    }
    double **result = malloc(m*sizeof(double*));
    for (int i = 0; i < m; i++)
    {
        result[i] = malloc(bn*sizeof(double));
    }

    for (int i = 0; i < m; i++)
    {
        for (int ia = 0; ia < bn; ia++)
        {
            double r = 0;
            for (int ib = 0; ib < n; ib++)
            {
                r = r + a[i][ib]*b[ib][ia];
            }
            result[i][ia] = r;
        }
    }

    return result;
}

double **transpose(double **a, int m, int n)
{
    double **result = malloc(n*sizeof(double*));
    for (int i = 0;i < n; i++)
    {
        result[i] = malloc(m*sizeof(double));
    }
    for (int i = 0; i < n; i++)
    {
        for (int ia = 0; ia < m; ia++)
        {
            result[i][ia] = a[ia][i];
        }
    }

    return result;
}

double **trans_multiply(double **a, double **t, int m, int n, int tm, int tn)
{
    double **result = malloc(m*sizeof(double*));
    for (int i = 0; i < m; i++)
    {
        result[i] = malloc(tm*sizeof(double));
    }

    for (int i = 0; i < m; i++)
    {
        for (int ia = 0; ia < tm; ia++)
        {
            double r = 0;
            for (int ib = 0; ib < n; ib++)
            {
                r = r + a[i][ib]*t[ia][ib];
            }
            result[i][ia] = r;
        }
    }
    
    return result;
}

int main(int argc, char *argv[])
{
    float time = 0.0;
    clock_t start, end;
    double **norm_mult;
    double **trans_mult;
    double **result_mat;
    int m = atoi(argv[1]), n = atoi(argv[2]), bm = atoi(argv[3]), bn = atoi(argv[4]);
    char mode = argv[5][0];
    char specify = 'n';
    char save = 'n';
    if (argc >= 7) specify = argv[6][0];
    if (argc >= 8) save = argv[7][0];
    double **a = create_r_matrix(m, n);
    double **b = create_r_matrix(bm, bn);
    if (specify == 't' || mode == 'o') start = clock();

    if (mode == 'o')
    {
        norm_mult = norm_multiply(a, b, m, n, bm, bn);
    }
    else if (mode == 't')
    {
        double **trans_b = transpose(b, bm, bn);
        if (specify == 'n') start = clock();
        trans_mult = trans_multiply(a, trans_b, m, n, bn, bm);
    }
    
    end = clock();
    time = (float) (((end - start) + 0.0) / CLOCKS_PER_SEC);
    printf("Elapsed time: %fs\n", time);
    if (save == 'y')
    {
        FILE *fh;
        if (argc >= 9) fh = fopen(argv[8], "w+");
        else fh = fopen("result.csv", "w+");
        if (mode == 't') result_mat = trans_mult;
        else result_mat = norm_mult;
        FILE *fa = fopen("a_matrix.csv", "w+");
        FILE *fb = fopen("b_matrix.csv", "w+");
        for (int i = 0; i < m; i++)
        {
            for (int ia = 0; ia < n; ia++)
            {
                if (ia != n-1) fprintf(fa, "%lf;", a[i][ia]);
                else fprintf(fa, "%lf\n", a[i][ia]);
            }
        }
        for (int i = 0; i < bm; i++)
        {
            for (int ia = 0; ia < bn; ia++)
            {
                if (ia != bn-1) fprintf(fb, "%lf;", b[i][ia]);
                else fprintf(fb, "%lf\n", b[i][ia]);
            }
        }
        for (int i = 0; i < m; i++)
        {
            for (int ia = 0; ia < bn; ia++)
            {
                if (ia != bn-1) fprintf(fh, "%lf;", result_mat[i][ia]);
                else fprintf(fh, "%lf\n", result_mat[i][ia]);
            }
        }
        fclose(fa);
        fclose(fb);
        fclose(fh);
    }
    return 0;
}