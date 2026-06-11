-- | Раздел 7+: кондиционирование = residuation (библиотека: condTau, qHom)

demoResiduation :: IO ()
demoResiduation = do
  putStrLn "=== Razdel 7+: kondicionirovanie = residuation ==="
  let dom = [(z1, z2) | z1 <- [1,2::Int], z2 <- [1,2::Int]]
      tauJ :: (Int, Int) -> Double
      tauJ (1,1) = 1.0
      tauJ (2,1) = 0.6
      tauJ (1,2) = 0.4
      tauJ (2,2) = 0.4
      tauJ _     = 0.0
      z1s = [1,2]
      z2s = [1,2]
      marg = margZ2 dom tauJ
      cnd z1 z2 = condTau dom tauJ z2 z1
  mapM_ (\(z1,z2) -> putStrLn $ "  tau(" ++ show z1 ++ "|" ++ show z2 ++ ") = "
         ++ show (cnd z1 z2)) [(a,b) | b <- z2s, a <- z1s]
  let chkEq = and [ ui (min (cnd z1 z2) (marg z2)) =~ ui (tauJ (z1, z2))
                  | z1 <- z1s, z2 <- z2s ]
      gridD = map (\k -> fromIntegral k / 20) [0..20 :: Int]
      chkMax = and [ c <= cnd z1 z2 + 1e-9
                   | z1 <- z1s, z2 <- z2s, c <- gridD
                   , ui (min c (marg z2)) =~ ui (tauJ (z1, z2)) ]
      chkNorm = and [ ui (maximum [cnd z1 z2 | z1 <- z1s]) =~ ltop | z2 <- z2s ]
  putStrLn $ "  Reshenie uravneniya: " ++ show chkEq
  putStrLn $ "  Maksimalnost:        " ++ show chkMax
  putStrLn $ "  Normirovka sup=1:    " ++ show chkNorm
  putStrLn $ "  Adjointness [0,1]:   " ++ show (checkResiduationAdj gammaGrid)
  putStrLn $ "  Adjointness Bool:    " ++ show (checkResiduationAdj [False, True])

demoResiduation
