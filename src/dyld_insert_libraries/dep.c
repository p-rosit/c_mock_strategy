#include "dep.h"

int external_func(int a) {
    return internal_func(a);
}

int internal_func(int a) {
    return a + a;
}
