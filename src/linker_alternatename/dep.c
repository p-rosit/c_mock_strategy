#include "dep.h"

// Definitions of symbols bear the weight of the mocking strategy here. The
// approach that makes the strategy work is that the definition must be defined
// with a different name than the actual symbol. At the linking stage we will
// then tell the linker that if it is unable to resolve `external_func` (which
// it will because no such definition exists) it should try to find
// `real_external_func` (or `mock_external_func` in the case of a test build).

int real_external_func(int a) {
    return internal_func(a);
}

int real_internal_func(int a) {
    return a + a;
}
