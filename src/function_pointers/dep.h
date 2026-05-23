#ifndef DEP_H
#define DEP_H

// The whole point of the struct is to be able to replace the symbols when
// testing, therefore we need to be able to turn of the const-ness when testing
#ifdef TEST_BUILD
    #define API_CONST
#else
    #define API_CONST const
#endif

struct DepVTable {
    int (*external_func)(int a);
    int (*internal_func)(int a);
};

// This takes the place of a normal set of function headers. Making this struct
// of functions pointers const is very important, if you additionally enable LTO
// the compiler will be able to just call the functions directly.
extern API_CONST struct DepVTable dep;

#endif
