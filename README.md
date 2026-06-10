# Mocking Functions in C

This repository contains contains a few different ways to mock functions in the `C` language. The strategies can be split into three major categories of approaches:

* Compile-time interception
    * [Macro function-like](src/macro_function_like/test_macro_function_like.py)
    * [Macro object-like](src/macro_object_like/test_macro_object_like.py)
    * [Function pointers](src/function_pointers/test_function_pointers.py)
* Link-time interception
    * [Object copy](src/objcopy/test_objcopy.py)
    * [Linker wrap](src/linker_wrap/test_linker_wrap.py)
    * [Linker alternatename](src/linker_alternatename/test_linker_alternatename.py)
* Runtime interception
    * [LD_PRELOAD](src/ld_preload/test_ld_preload.py)
    * [DYLD_INSERT_LIBRARIES](src/dyld_insert_libraries/test_dyld_insert_libraries.py)

I have implemented these strategies in an effort to figure out how to test [tdo](https://github.com/p-rosit/tdo) which is a dynamic test runner. I wanted to know how it would behave under system resource limits but as far as I can tell there's nowhere to read on pros and cons between different function interception strategies.

Below is a summary table of each mocking strategy:

| Method                                                                            | Can Mock Internal Calls? | Can Replace Function Pointers? | Is Portable? | Can Mock Precompiled Dependencies | Can chain mocks | Requires Restructuring Code? |
| --------------------------------------------------------------------------------- | ------------------------ | ------------------------------ | ------------ | --------------------------------- | --------------- | ---------------------------- |
| [Macro function-like](src/macro_function_like/test_macro_function_like.py)        | Yes                      | No                             | Yes          | No                                | Yes             | Yes                          |
| [Macro object-like](src/macro_object_like/test_macro_object_like.py)              | No                       | Yes                            | Yes          | Yes                               | Yes             | No                           |
| [Function pointers](src/function_pointers/test_function_pointers.py)              | Yes                      | Yes                            | Yes          | No                                | Yes             | Yes                          |
| [Object copy](src/objcopy/test_objcopy.py)                                        | No                       | Yes                            | Yes          | Yes                               | Yes             | No                           |
| [Linker wrap](src/linker_wrap/test_linker_wrap.py)                                | No                       | Yes                            | No           | Yes                               | No              | No                           |
| [Linker alternatename](src/linker_alternatename/test_linker_alternatename.py)     | No                       | Yes                            | No           | No                                | Yes             | Yes                          |
| [LD_PRELOAD](src/ld_preload/test_ld_preload.py)                                   | No                       | Yes                            | No           | Yes                               | Yes             | No                           |
| [DYLD_INSERT_LIBRARIES](src/dyld_insert_libraries/test_dyld_insert_libraries.py)  | No                       | Yes                            | No           | Yes                               | Yes             | No                           |

