#include <stdio.h>
#include "dep.h"

struct DepVTable real = {
    .external_func = NULL,
    .internal_func = NULL,
};

int mock_external_func(int a) {
    int r = real.external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}

int real_main(int argc, char **argv);
int main(int argc, char **argv) {
    // symbol setup
    real = dep;
    dep.external_func = mock_external_func;
    // real main
    return real_main(argc, argv);
}
