#include "dep.h"

int external_func(int a);
int internal_func(int a);

struct DepVTable dep = {
    .external_func = external_func,
    .internal_func = internal_func,
};

int external_func(int a) {
    // As long as we call functions through the namespace struct we will be
    // able to intercept any call, even these calls within a translation unit
    return dep.internal_func(a);
}

int internal_func(int a) {
    return a + a;
}
