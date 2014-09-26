"""
My take and tweaks for the cpp magic.
This magic function lets you run a c/c++ file inside an ipython notebook cell
based on:
  http://nbviewer.ipython.org/github/rossant/ipython-minibook/blob/master/chapter6/602-cpp.ipynb
"""
import IPython.core.magic as ipym
import os
import subprocess

@ipym.magics_class
class CppMagics(ipym.Magics):
  @ipym.cell_magic
  def cpp(self, line, cell=None):
    """Compile, execute C++ code, and return the standard output."""
    # Define the source and executable filenames. (Change this to get output in
    # the future)
    source_filename = 'temp.cpp'
    program_filename = 'temp.exe'
    # Write the code contained in the cell to the C++ file temp.cpp
    with open(source_filename, 'w') as f:
      f.write(cell)
    # Compile the C++ code into an executable, if it didnt work return the error
    try:
      out_comp_try = subprocess.check_output(["g++ temp.cpp -o temp.exe"],shell=True)
    except subprocess.CalledProcessError as e:
      if e.returncode==1:
        output =  "We had some sort of problem compiling the program , check the \n kernel window for the exact compiler errors and warning "
        return output
    proc_comp = subprocess.Popen(["g++ temp.cpp -o temp.exe"], stdout=subprocess.PIPE,shell=True)
    (out_comp, err_comp) = proc_comp.communicate()
    proc_run = subprocess.Popen(["./temp.exe"], stdout=subprocess.PIPE,shell=True)
    (out_run, err_run) = proc_run.communicate()
    # Cleanup the executable
    os.system("rm temp.exe")
    output = out_run
    return output

def load_ipython_extension(ipython):
  ipython.register_magics(CppMagics)
