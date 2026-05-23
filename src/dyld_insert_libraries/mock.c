#include <stdio.h>
#include <mach-o/dyld-interposing.h>
#include "dep.h"

int mock_external_func(int a) {
    // We have placed our mock symbol first in the queue with
    // `DYLD_INSERT_LIBRARIES`, to call the real function we don't need to do
    // anything special `DYLD_INTERPOSE` below takes care of avoiding the
    // infinite recursion
    int r = external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}

// Register our function as intercepting `external_func`
DYLD_INTERPOSE(mock_external_func, external_func);
