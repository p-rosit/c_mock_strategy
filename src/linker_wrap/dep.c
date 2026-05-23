#include "dep.h"

// This code is unaffected by the mocking strategy.

int external_func(int a) {
    return internal_func(a);
}

int internal_func(int a) {
    return a + a;
}
