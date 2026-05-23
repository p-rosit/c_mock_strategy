#include <stdio.h>

int real_external_func(int a);
int mock_external_func(int a) {
    int r = real_external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
