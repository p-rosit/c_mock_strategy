#include <stdio.h>
#include "dep.h"

// All the complexity of this mocking strategy has been offloaded to the
// building step. The files need to be compiled separately and then the symbol
// being mocked will be renamed in every object file except the one it's
// defined in.
int wrap_external_func(int a) {
    int r = external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
