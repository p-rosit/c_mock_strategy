#include "dep.h"

int main() {
    // Function calls look the same as normal, both function calls between
    // translation units as well as function calls within translation units
    // can be replaced. A drawback, however, is that function pointers will
    // not be correctly replaced:
    //
    // ```
    // func = external_func;
    // func();
    // ```
    //
    // would not be intercepted by the mock function.
    return external_func(5);
}
