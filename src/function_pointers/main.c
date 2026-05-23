#include "dep.h"

int main() {
    // This testing strategy affects every single caller of the functions
    // we've defined. It does give a rudimentary form of namespacing but it
    // completely kills inlining and makes every function call unknown.
    //
    // This can be mitigated by defining the namespace struct as const and
    // enabling LTO. By enabling LTO (and making it const) the compiler is
    // still able to make the function calls known as if you wrote a direct
    // function call.
    return dep.external_func(5);
}
