
/* 
A* -------------------------------------------------------------------
B* This file contains source code for the PyMOL computer program
C* copyright 1998-2000 by Warren Lyford Delano of DeLano Scientific. 
D* -------------------------------------------------------------------
E* It is unlawful to modify or remove this copyright notice.
F* -------------------------------------------------------------------
G* Please see the accompanying LICENSE file for further information. 
H* -------------------------------------------------------------------
I* Additional authors of this source file include:
-* 
-* 
-*
Z* -------------------------------------------------------------------
*/
#ifndef _H_GadgetSet
#define _H_GadgetSet

#include"Rep.h"
#include"Setting.h"
#include"CGOStruct.h"

typedef struct GadgetSet {
  // methods (not fully refactored yet)
  void fFree();

  // methods
  void update();
  void render(RenderInfo * info);
  void invalidateRep(int type, int level);

  PyMOLGlobals *G;
  struct ObjectGadget *Obj;     /* NOT pickled -- restore manually */
  int State;                    /* NOT pickled -- restore manually */
  float *Coord;
  float *Normal;
  float *Color;
  int NCoord;
  int NNormal;
  int NColor;

  Pickable *P;
  CGO *PickShapeCGO;
  CGO *PickCGO;
  CGO *StdCGO;
  CGO *ShapeCGO;
  CSetting *Setting;
} GadgetSet;

#include"ObjectGadget.h"

GadgetSet *GadgetSetNew(PyMOLGlobals * G);
PyObject *GadgetSetAsPyList(GadgetSet * I);
int GadgetSetFromPyList(PyMOLGlobals * G, PyObject * list, GadgetSet ** cs, int version);
int GadgetSetGetExtent(GadgetSet * I, float *mn, float *mx);
int GadgetSetGetVertex(GadgetSet * I, int index, int base, float *v);
int GadgetSetSetVertex(GadgetSet * I, int index, int base, float *v);
#endif
