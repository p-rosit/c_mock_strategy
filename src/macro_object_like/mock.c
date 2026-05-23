#include <stdio.h>
#include "dep.h"

int mock_external_func(int a) {
    // The real symbol can be called directly
    int r = external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
