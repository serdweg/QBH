//TOF
#include <climits>

#include "Pythia8/Pythia.h"
using namespace Pythia8; 

#include "qbh.h"
using namespace QBH; 

#include "HistClass.hh"
#include "TFile.h"
#include "TLorentzVector.h"

void init();

void terminate(int status);

bool OUTPUT;

Pythia* pythia;

QuantumBlackHole* qbh;

dLHAup* lhaPtr;

int all_events;
int sel_events;
