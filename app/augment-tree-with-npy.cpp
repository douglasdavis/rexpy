#include "CLI11.hpp"
#include "cnpy.h"

#include <TTree.h>
#include <TFile.h>

#include <string>

template <typename T>
void augment_tree(TTree* tree, const T* data, const char* name) {
  float val;
  TBranch *new_branch = tree->Branch(name, &val);
  auto nentries = tree->GetEntries();
  for (Long64_t i = 0; i < nentries; ++i) {
    val = static_cast<float>(data[i]);
    new_branch->Fill();
  }
}

bool has_branch(TTree* tree, const char* name) {
  return tree->GetListOfBranches()->Contains(name);
}

int main(int argc, char *argv[]) {
  CLI::App app("augment-tree-with-npy");
  std::string file_name;
  std::string tree_name;
  std::string npyf_name;
  std::string branch_name = "pybdt_response";

  app.add_option("file", file_name, "ROOT file to augment")->required()->check(CLI::ExistingFile);
  app.add_option("tree", tree_name, "ROOT tree in the file to augment")->required();
  app.add_option("npyf", npyf_name, "The NumPy .npy file that will be the branch")->required()->check(CLI::ExistingFile);
  app.add_option("-b, --branch-name", branch_name, "the name for the BDT response branch");

  CLI11_PARSE(app, argc, argv);

  auto numpy_array = cnpy::npy_load(npyf_name);
  const double* numpy_data = numpy_array.data<double>();
  auto file = TFile::Open(file_name.c_str(), "UPDATE");
  auto tree = dynamic_cast<TTree*>(file->Get(tree_name.c_str()));
  if (static_cast<Long64_t>(numpy_array.num_vals) != tree->GetEntries()) {
    std::cerr << "NumPy array and TTree have different lengths, exiting gracefully" << std::endl;
    return 0;
  }
  if (has_branch(tree, branch_name.c_str())) {
    std::cout << "Branch already exists in tree, exiting gracefully" << std::endl;
    return 0;
  }
  augment_tree(tree, numpy_data, branch_name.c_str());
  tree->Write(0, TObject::kOverwrite);
  file->Close();

  return 0;
}
