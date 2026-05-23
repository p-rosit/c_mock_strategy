#include "dep.h"

// This file is not affected by the testing strategy at all, we define normal
// functions here. The work needed to do the symbol replacement is offloaded
// to the test build process.

int external_func(int a) {
    return internal_func(a);
}

int internal_func(int a) {
    return a + a;
}
