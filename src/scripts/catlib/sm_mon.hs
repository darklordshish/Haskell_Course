-- | Раздел 17: монада возможности — из библиотеки (../lib/Distribution.hs)

data W = Sun | Rain | Fog deriving (Show, Eq, Ord)

stepW :: W -> Poss W
stepW Sun  = possOf [(Sun, 1.0), (Fog, 0.4), (Rain, 0.2)]
stepW Rain = possOf [(Rain, 1.0), (Fog, 0.7), (Sun, 0.3)]
stepW Fog  = possOf [(Fog, 1.0), (Sun, 0.6), (Rain, 0.6)]

demoPossMonad :: IO ()
demoPossMonad = do
  putStrLn "=== Razdel 17: monada vozmozhnosti (i ne tolko) ==="
  let m0 = possOf [(Sun, 1.0), (Rain, 0.5)]
      k2 w = possOf [(w, 1.0), (Fog, 0.5)]
  putStrLn $ "  [Poss]  zakony monady: " ++ show (checkMonadLaws m0 stepW k2 Sun)
  putStrLn $ "  sup posle bind = " ++ show (supPoss (bindD m0 stepW))
  mapM_ (\n -> putStrLn $ "  " ++ show n ++ " shagov ot Sun: "
               ++ showDistList (nStepsD n stepW Sun)) [1, 2, 3]
  putStrLn $ "  Stabilizaciya sup-min stepenej: "
             ++ show (eqDist (nStepsD 3 stepW Sun) (nStepsD 4 stepW Sun))
  -- ТА ЖЕ монада над вероятностным полукольцом: одна математика, две теории
  let stepP :: W -> Dist ProbW W
      stepP Sun  = distOf [(Sun, ProbW 0.7), (Fog, ProbW 0.2), (Rain, ProbW 0.1)]
      stepP Rain = distOf [(Rain, ProbW 0.5), (Fog, ProbW 0.3), (Sun, ProbW 0.2)]
      stepP Fog  = distOf [(Fog, ProbW 0.4), (Sun, ProbW 0.3), (Rain, ProbW 0.3)]
      etaP w = distOf [(w, ProbW 1.0)]
  putStrLn $ "  [ProbW] zakony monady: "
             ++ show (checkMonadLaws (etaP Sun) stepP etaP Sun)
  putStrLn $ "  [ProbW] 2 shaga: " ++ showDistList (nStepsD 2 stepP Sun)
  -- И над Bool: семантика достижимости
  let stepB :: W -> Dist Bool W
      stepB Sun  = distOf [(Sun, True), (Fog, True)]
      stepB Rain = distOf [(Rain, True)]
      stepB Fog  = distOf [(Fog, True), (Rain, True)]
  putStrLn $ "  [Bool] dostizhimost za 2 shaga iz Sun: "
             ++ showDistList (nStepsD 2 stepB Sun)

demoPossMonad
