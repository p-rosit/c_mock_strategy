#include "dep.h"

int main() {
    // Only symbols in different translation units can be mocked when you're
    // using object-like macro replacement.
    //
    // In particular only function calls made to symbols in different
    // translation units can be replaced
    return external_func(5);
}
