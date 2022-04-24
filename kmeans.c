#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

void invalid_input()
{
    printf("Invalid Input!\n");
    exit(0);
}

void other_error()
{
    printf("An Error Has Occurred\n");
    exit(0);
}

double distance(double const *u, double const *v, int length)
{
    double d = 0;
    for (int i = 0; i < length; i++)
        d += (u[i] - v[i]) * (u[i] - v[i]);

    return sqrt(d);
}

// sum the second vector v into u
void points_sum(double *u, double const *v, int length)
{
    for (int i = 0; i < length; i++)
        u[i] += v[i];
}

double **k_means(int const K, int const max_iter, double **points, int const points_length, int const point_length)
{
    // initialise centroids array of points.(each point is array)
    double **centroids = calloc(K, sizeof(double *));
    for (int i = 0; i < K; i++)
    {
        centroids[i] = calloc(point_length, sizeof(double));
        for (int j = 0; j < point_length; j++)
        {
            centroids[i][j] = points[i][j];
        }
    }

    // each index represent point number and the cell content is its centoird index
    int *points_to_centroids = calloc(points_length, sizeof(int));
    int *diff_small = calloc(K, sizeof(int));
    for (int i = 0; i < K; i++)
    {
        diff_small[i] = 1;
    }

    for (int l = 0; l < max_iter; l++)
    {
        // iterating points and update their centorid's index
        for (int i = 0; i < points_length; i++)
        {
            int new_centroids_index = points_to_centroids[i];
            for (int j = 0; j < K; j++)
            {
                if (distance(points[i], centroids[j], point_length) < distance(points[i], centroids[new_centroids_index], point_length))
                {
                    new_centroids_index = j;
                }
            }
            points_to_centroids[i] = new_centroids_index;
        }

        // calculating new centroids
        for (int i = 0; i < K; i++)
        {
            diff_small[i] = 0;
            double *avg_centroid = calloc(point_length, sizeof(double));
            double counter = 0;
            for (int j = 0; j < points_length; j++)
            {
                if (points_to_centroids[j] == i)
                {
                    points_sum(avg_centroid, points[j], point_length);
                    counter++;
                }
            }

            if (counter > 0)
            {
                for (int k = 0; k < point_length; k++)
                    avg_centroid[k] = avg_centroid[k] / counter;

                if (distance(centroids[i], avg_centroid, point_length) < 0.001)
                {
                    diff_small[i] = 1;
                }
                free(centroids[i]);
                centroids[i] = avg_centroid;
            }
        }
        int all_diffs_are_small = 0;
        for (int k = 0; k < K; k++)
        {
            all_diffs_are_small += diff_small[k];
        }
        if (all_diffs_are_small == K)
        {
            break;
        }
    }
    // free memory and return result
    free(points_to_centroids);
    free(diff_small);
    return centroids;
}

// check if string is number
int is_number(char s[])
{
    for (int j = 0; j < strlen(s); j++)
        if (!isdigit(s[j]))
            return 0;
    return 1;
}

int is_valid_path(char *s)
{
    int dot_flag = 0;
    for (char c = *s; c != '\0'; c = *++s)
    {
        if (c == '.')
        {
            dot_flag = 1;
            if (strcmp(++s, "txt") != 0)
                return 0;
        }
    }
    if (!dot_flag)
        return 0;
    return 1;
}

int main(int argc, char **argv)
{
    int K;
    int max_iter = 200;
    char *input_path;
    char *output_path;

    if (argc != 4 && argc != 5)
        invalid_input();

    if (argc == 4)
    {
        if (is_number(argv[1]))
        {
            K = atoi(argv[1]);
            input_path = argv[2];
            output_path = argv[3];
            if (!is_valid_path(input_path) || !is_valid_path(output_path))
                invalid_input();
        }
        else
        {
            invalid_input();
        }
    }
    if (argc == 5)
    {
        if (is_number(argv[1]) && is_number(argv[2]))
        {
            K = atoi(argv[1]);
            max_iter = atoi(argv[2]);
            input_path = argv[3];
            output_path = argv[4];
            if (!is_valid_path(input_path) || !is_valid_path(output_path))
                invalid_input();
        }
        else
        {
            invalid_input();
        }
    }

    FILE *fptr = fopen(input_path, "r");
    if (fptr == NULL)
    {
        other_error();
    }

    int point_size = 0;
    int points_length = 0;
    char c;

    // counting point size
    while ((c = fgetc(fptr)) != EOF)
    {
        double point;
        if (c == '\n')
        {
            rewind(fptr);
            break;
        }
        point_size++;
        fscanf(fptr, "%lf", &point);
    }

    // counting number of points
    while ((c = fgetc(fptr)) != EOF)
        if (c == '\n')
            points_length++;

    rewind(fptr);

    // checking if K < number of points
    if (K > points_length)
        invalid_input();

    double **points = calloc(points_length, sizeof(double *));
    // reading the points from the file into array
    for (int i = 0; i < points_length; i++)
    {
        points[i] = calloc(point_size, sizeof(double));
        for (int j = 0; j < point_size; j++)
        {
            fscanf(fptr, "%lf", &points[i][j]);
            char c = fgetc(fptr);
        }
    }
    fclose(fptr);

    double **centroids = k_means(K, max_iter, points, points_length, point_size);

    // writing centroids into output file
    fptr = fopen(output_path, "w");
    if (fptr == NULL)
    {
        other_error();
    }
    for (int i = 0; i < K; i++)
    {
        for (int j = 0; j < point_size; j++)
        {
            if (j == point_size - 1)
                fprintf(fptr, "%.4lf\n", centroids[i][j]);
            else
                fprintf(fptr, "%.4lf,", centroids[i][j]);
            char c = fgetc(fptr);
        }
    }

    fclose(fptr);

    // free memory
    for (int i = 0; i < K; i++)
        free(centroids[i]);
    free(centroids);
    for (int i = 0; i < points_length; i++)
        free(points[i]);
    free(points);

    return 0;
}
