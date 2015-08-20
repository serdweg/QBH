#include "main.hh"

/*****************************************************************************/
/** Init function.                                                           */
/*****************************************************************************/
void init() {
    /// Output LHEF file.
    OUTPUT = true;

    /// Declare Pythia object.
    pythia = new Pythia();

    /// Declare and initialize quantum black hole object.
    bool initialize = true;
    qbh = new QuantumBlackHole(pythia,initialize);

    /// Decalare derived LHA user process object.
    lhaPtr = new dLHAup;

    pythia->setLHAupPtr(lhaPtr);

    /// Initialize the necessary control histograms
    HistClass::CreateHisto("pt_ele", 6000, 0, 6000, "p_{T}(ele) (GeV)");
    HistClass::CreateHisto("eta_ele", 60, -3, 3, "#eta(ele)");
    HistClass::CreateHisto("phi_ele", 65, -3.25, 3.25, "#phi(ele) (rad)");
    HistClass::CreateHisto("pt_muo", 6000, 0, 6000, "p_{T}(muo) (GeV)");
    HistClass::CreateHisto("eta_muo", 60, -3, 3, "#eta(muo)");
    HistClass::CreateHisto("phi_muo", 65, -3.25, 3.25, "#phi(muo) (rad)");
    HistClass::CreateHisto("pt_qbh", 6000, 0, 6000, "p_{T}(qbh) (GeV)");
    HistClass::CreateHisto("eta_qbh", 60, -3, 3, "#eta(qbh)");
    HistClass::CreateHisto("phi_qbh", 65, -3.25, 3.25, "#phi(qbh) (rad)");
    HistClass::CreateHisto("mass_qbh", 6000, 0, 6000, "M(qbh) (GeV)");

    all_events = 0;
    sel_events = 0;
}

void terminate(int status, char *argv[]) {
    /// Termination.
    pythia->stat();
  
    if (OUTPUT) {
        (void)lhaPtr->closeLHEF();
        /// Write QBH banner information to QBHfile.lhe
        qbh->trailer(((string)"QBH").append(argv[5]));
    }

    /// Time job exectution.
    long t = clock();
    double dt = (double)t;
    if (t < 0) dt += 2.0 * (double)LONG_MAX;
    long min = (long)((dt/(double)CLOCKS_PER_SEC) / 60.0);
    long sec = (long)(dt/(double)CLOCKS_PER_SEC) % 60;
    printf("\nProcessing time %ld min %ld sec\n",min,sec);

    if (status) {
        printf("Normal sucessful completion.\n\n");
    } else {
        printf("Possible execution problem.\n\n");
    }

    std::cout << std::endl << "\t e-mu fraction: " << (double)sel_events/(double)all_events << std::endl << std::endl;

    std::cerr << "creating file\n";
    TFile* out_file = new TFile("test.root", "RECREATE");
    HistClass::Write("pt_ele");
    HistClass::Write("eta_ele");
    HistClass::Write("phi_ele");
    HistClass::Write("pt_muo");
    HistClass::Write("eta_muo");
    HistClass::Write("phi_muo");
    HistClass::Write("pt_qbh");
    HistClass::Write("eta_qbh");
    HistClass::Write("phi_qbh");
    HistClass::Write("mass_qbh");
    out_file->Close();
    std::cerr << "done\n";

    /// <n_extra_dimension> <threshold_mass> <RS_or_PDG> <xs> <sigma(xs)> <BR> <out_file_name> <n_events>
    std::ofstream outfile;
    outfile.open("info.txt", std::ios_base::app);
    outfile << atoi(argv[2]) << "\t" << atof(argv[3]) << "\t" << argv[4] << "\t" << pythia->info.sigmaGen() << "\t" << pythia->info.sigmaErr() << "\t" << (double)sel_events/(double)all_events << "\t" << argv[5] << "\t" << atoi(argv[1]) << std::endl;
    outfile.close();
}

/*****************************************************************************/
/** Event generator code (main program).                                     */
/*****************************************************************************/
int main(int argc, char *argv[]) {
    bool status;

    if (argc != 6) {
        std::cerr << "Not the right number of arguments!" << std::endl;
        std::cerr << "Usage:" << std::endl;
        std::cerr << "./qbh <n_events> <n_extra_dimension> <threshold_mass> <RS_or_PDG> <out_file_name>" << std::endl;
        std::cerr << std::endl;
        std::cerr << "cancelling!" << std::endl;
        return 42;
    }

    init();

    pythia->readString("Beams:frameType = 5");

    /// Number of events to be produced
    int n_events = atoi(argv[1]);
    pythia->readString("Main:NumberOfEvents = 10000000");

    /// QCD scale definition
    qbh->setQscale(true); /// Definition of QCD scale for PDFs false(= QBH mass), true (= inverse gravitational radius) (Default = true)

    /// Yoshino-Rychkov stuff
    qbh->setYRform(false); /// Use YR-factors (Default = false)
    qbh->setTrap(false); /// User YR trapped surface calculation (Default = false)

    /// SM symmetries
    qbh->setSM(false); /// Conserve global symmetries (Default = true)

    /// Majorana neutrinos
    qbh->setMajorana(false); /// neutrinos are majorana (true) or dirac (false) (Default = false) 

    /// Neutrino handedness
    qbh->setChiral(true); /// neutrinos are left-handed only (false) or left and right-handed (true) (Default = true)

    /// Higgs
    qbh->setHiggs(false); /// Include Higgs as allowed particle (Default = true)

    /// Graviton
    qbh->setGraviton(false); /// Include Graviton as allowed particle (Default = true)

    /// Totel number of dimensions
    qbh->setTotdim(4 + atoi(argv[2])); /// Total number of spacetime dimensions 5-11 allowed (Default = 10)

    /// Planck scale definition
    /// RS or ADD black hole
    if (strcmp(argv[4], (char*)"RS") == 0) {
        qbh->setPlanckdef(1); /// Definition of the planck scale 1 (= Randall-Sundrum), 2 (= Dimopoulos-Landsberg), 3 (= PDG), else (= Giddings-Thomas definition) (Default = 3)
        qbh->setRS1(false); /// false (= ADD black hole), true (= Randall-Sundrum type-1 black hole) (Default = false)
    } else if (strcmp(argv[4], (char*)"PDG") == 0) {
        qbh->setPlanckdef(3);
        qbh->setRS1(false);
    } else {
        std::cerr << "The value for the <RS_or_PDG> parameter is unknown!" << std::endl;
        std::cerr << "The allowed values are 'RS' and 'PDG'" << std::endl;
        std::cerr << "Your value: " << argv[4] << std::endl;
        std::cerr << std::endl;
        std::cerr << "cancelling!" << std::endl;
        return 42;
    }

    double threshold_mass = atof(argv[3]);

    /// Planck mass
    qbh->setMplanck(threshold_mass); /// fundamental planck scale (Default = 1000)

    /// Electric charge
    qbh->setQstate(0); /// Three time electric charge [-4,-3,-2,-1,0,1,2,3,4] allowed, 9 for all partons (Default = 9)

    /// Initial state
    qbh->setIstate(0); /// Initial state 0 (q-q), 1 (q-g), 2 (g-g), 3 (all) (Default = 3)

    /// Min QBH mass
    qbh->setMinmass(threshold_mass); /// Minimum quantum black hole mass (Default = 1000)

    /// Max QBH mass
    qbh->setMaxmass(14000); /// Maximum qunatum black hole mass (Default = 14000)

    /// Center of mass energy
    qbh->setEcm(13000); /// Proton-proton center of mass energy (Default = 14000)

    /// Initialize PDFs.
    qbh->setLHAglue(10042);  ///CTEQ6L1
    // qbh->setLHAglue(192800); ///NNPDF21_100
    // qbh->setLHAglue(10800);  ///CT10
    // qbh->setLHAglue(10550);  ///CTEQ6.6
    // qbh->setLHAglue(19050);  ///CTEQ5M
    // qbh->setLHAglue(21000);  ///MSTW2008lo
    // qbh->setLHAglue(29041);  ///MRST98lo fit
    // qbh->setLHAglue(0);      ///PYTHIA internal

    /// Set some PYTHIA switches.
    (void)pythia->readString("SoftQCD:nonDiffractive = off");
    (void)pythia->readString("SoftQCD:all       = off");
    (void)pythia->readString("PartonLevel:ISR   = off");
    (void)pythia->readString("PartonLevel:FSR   = off");
    (void)pythia->readString("PartonLevel:MPI    = off");
    (void)pythia->readString("HadronLevel:all   = off");
    (void)pythia->readString("Check:history     = on");
    (void)pythia->readString("Check:nErrList    = 10");

    if (OUTPUT) (void)lhaPtr->openLHEF(((string)"LHEF").append(argv[5]));

    /// Initialize Pythia object.
    status = pythia->init();

    if (OUTPUT) (void)lhaPtr->initLHEF();  
    delete qbh;

    /// Loop over events.
    if (status) {
        for (int iEvent=0;iEvent<pythia->mode("Main:numberOfEvents"); ++iEvent) {

            /// Generate event.
            status = pythia->next();
            if (!status) continue;

            /// Event listing.
            if (iEvent < pythia->mode("Next:numberShowEvent")) {
                //pythia->info.list();
                pythia->process.list();
                //pythia->event.list();
            }

            all_events++;
            if ((abs(pythia->process[5].id()) == 11 and abs(pythia->process[6].id()) == 13) or (abs(pythia->process[5].id()) == 13 and abs(pythia->process[6].id()) == 11)) {
                sel_events++;
                TLorentzVector* ele_vec = new TLorentzVector();
                TLorentzVector* muo_vec = new TLorentzVector();
                TLorentzVector* qbh_vec = new TLorentzVector();
                if (abs(pythia->process[5].id()) == 11) {
                    ele_vec->SetPxPyPzE(pythia->process[5].px(),pythia->process[5].py(),pythia->process[5].pz(),pythia->process[5].e());
                    muo_vec->SetPxPyPzE(pythia->process[6].px(),pythia->process[6].py(),pythia->process[6].pz(),pythia->process[6].e());
                } else {
                    ele_vec->SetPxPyPzE(pythia->process[6].px(),pythia->process[6].py(),pythia->process[6].pz(),pythia->process[6].e());
                    muo_vec->SetPxPyPzE(pythia->process[5].px(),pythia->process[5].py(),pythia->process[5].pz(),pythia->process[5].e());
                }
                *qbh_vec = *ele_vec + *muo_vec;
                HistClass::Fill("pt_ele", ele_vec->Pt(), 1);
                HistClass::Fill("eta_ele", ele_vec->Eta(), 1);
                HistClass::Fill("phi_ele", ele_vec->Phi(), 1);
                HistClass::Fill("pt_muo", muo_vec->Pt(), 1);
                HistClass::Fill("eta_muo", muo_vec->Eta(), 1);
                HistClass::Fill("phi_muo", muo_vec->Phi(), 1);
                HistClass::Fill("pt_qbh", qbh_vec->Pt(), 1);
                if (qbh_vec->Pt() == 0) {
                    HistClass::Fill("eta_qbh", 0, 1);
                    HistClass::Fill("phi_qbh", 0, 1);
                } else {
                    HistClass::Fill("eta_qbh", qbh_vec->Eta(), 1);
                    HistClass::Fill("phi_qbh", qbh_vec->Phi(), 1);
                }
                HistClass::Fill("mass_qbh", qbh_vec->M(), 1);

                if (OUTPUT) (void)lhaPtr->eventLHEF(false);
            }

            if (sel_events == n_events)break;
        } /// End of event loop.
    }

    terminate(status, argv);

    return status;
}
/*****************************************************************************/
///EOF

