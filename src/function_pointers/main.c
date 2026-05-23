#include "dep.h"

int main() {
    // This testing strategy affects every single caller of the functions
    // we've defined. It does give a rudimentary form of namespacing but it
    // completely kills inlining and makes every function call unknown.
    return dep.external_func(5);
}
