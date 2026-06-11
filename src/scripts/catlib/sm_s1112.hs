-- | Разделы 11-12: энтропии и идентификация — из библиотеки

smE :: SubjModel Int
smE = dualConsistent [1,2,3] (\x -> case x of { 1 -> 1.0; 2 -> 0.7; _ -> 0.3 })

demoS1112 :: IO ()
demoS1112 = do
  putStrLn "=== Razdely 11-12: entropii i identifikaciya ==="
  putStrLn $ "  Informativnost    = " ++ show (subjInformativity smE)
  putStrLn $ "  Neopredelennost   = " ++ show (subjUncertainty smE)
  putStrLn $ "  Dvojnaya entropiya = " ++ show (dualEntropy smE)
  putStrLn $ "  Entropiya 3-go var = " ++ show (thirdVariantEntropy smE)
  let ign = absoluteIgnorance [1,2,3::Int]
  putStrLn $ "  Neznanie: Inf=" ++ show (subjInformativity ign)
             ++ " Neopr=" ++ show (subjUncertainty ign)
  let obs k z = if k == z then 1.0 else 0.3 :: Double
      loss k d = if k == d then 0.0 else 0.8 :: Double
  putStrLn "  Optimalnoe pravilo identifikacii:"
  mapM_ (\(z, d) -> putStrLn $ "    d*(" ++ show z ++ ") = " ++ show d)
        (optimalDecision [1,2] [1,2] obs loss)

demoS1112
