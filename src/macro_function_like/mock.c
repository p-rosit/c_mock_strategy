#include <stdio.h>
#include "dep.h"

int (external_func)(int a);

int mock_external_func(int a) {
    // If one wants to call the real function it must be written as
    // `(external_func)` to circumvent the macro replacement
    int r = (external_func)(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
