# Secure-MPPH
 Secure-MPPH stands for Secure Multi-Party Perceptual Hash. The block-mean value perceptual hash algorithm is secured by Yao's garbling circuit. 



## This Repository Uses Submodules for Dependencies
Secure-MPPH draws upon [libscapi](https://github.com/cryptobiu/libscapi)  and [phash](https://github.com/clearscene/pHash) which are both 3rd party C++ libraries. Note: we use a [forked version of phash](https://github.com/dahadaller/pHash) in order to incorporate the block mean hash algorithm implemented [here.](https://gist.github.com/stereomatchingkiss/6b9034f72850b518f63631852d7b636f)  So, to properly clone this library, issue the following commands after `git clone https://github.com/timashana/Secure-MPPH.git` :

```bash
git submodule init
git submodule update
```

the submodules will then download into the `libraries/libscapi` and `libararies/phash` folders. Without this step, the `libraries` folder will remain empty and all code dependent on the non-stl libraries will not function. For more information about submodules check the [git-scm documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules).