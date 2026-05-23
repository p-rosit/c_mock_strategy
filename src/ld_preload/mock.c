#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include "dep.h"

int external_func(int a) {
    // We have placed our mock symbol first in the queue with `LD_PRELOAD`,
    // to call the real function we can just find the next one in the queue.
    int (*real_func)(int) = dlsym(RTLD_NEXT, "external_func");
    int r = real_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
