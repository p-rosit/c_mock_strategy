#include "dep.h"

int main() {
    // This code as well as the definition of the symbols look identical to
    // "normal" code, the effort in the strategy has been offloaded to the
    // test build process.
    return external_func(5);
}
