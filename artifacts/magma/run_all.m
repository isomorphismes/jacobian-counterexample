print "Magma version:", GetVersion();
load "01_direct_verification.m";
load "02_structural_certificate.m";
load "03_fiber_certificate.m";
load "04_normalization_certificate.m";
load "05_binary_cubic_certificate.m";
load "06_plane_attack_certificates.m";
print "PASS: all Magma certificates completed.";
quit;
