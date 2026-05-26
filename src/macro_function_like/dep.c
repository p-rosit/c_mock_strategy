#include "dep.h"

// This file pays the price of the mocking strategy, the definitions need to
// avoid macro replacement by writing `(function_name)`. Note that if we
// compile the test build in multiple steps like in the `macro_object_like`
// strategy we could avoid writing `(function_name)` but we would lose a major
// benefit of even being able to mock `internal_func` which that strategy is
// unable to do.

int (external_func)(int a) {
    // Unlike the `macro_object_like` strategy this strategy can even intercept
    // function calls within translation units (like `internal_func`).
    return internal_func(a);
}

int (internal_func)(int a) {
    return a + a;
}
