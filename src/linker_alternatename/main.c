#include "dep.h"

int main() {
    // Only symbols called between translation units can be intercepted.
    return external_func(5);
}
