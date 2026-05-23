#include <stdio.h>

// The naming `__real_<name>` and `__wrap_<name>` is very important, it's
// the names the linker expects to find when you add the flag `--wrap=<name>`
int __real_external_func(int a);

int __wrap_external_func(int a) {
    int r = __real_external_func(a);
    fprintf(stderr, "Real result: %d\n", r);
    return a;
}
