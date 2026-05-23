#ifndef DEP_H
#define DEP_H

struct DepVTable {
    int (*external_func)(int a);
    int (*internal_func)(int a);
};

extern struct DepVTable dep;

#endif
