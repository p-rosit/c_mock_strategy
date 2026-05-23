#include "dep.h"

int main() {
    // Only symbols between translation units can be intercepted.
    return external_func(5);
}
