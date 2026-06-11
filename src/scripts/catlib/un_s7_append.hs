

-- Параллель из библиотеки (../lib/Distribution.hs): та же цепь над
-- полукольцом возможности (sup-min) вместо (+,*) — один bindD, две теории.
wkPoss :: Weather7 -> D.Poss Weather7
wkPoss Sunny7  = D.possOf [(Sunny7, 1.0), (Cloudy7, 0.3), (Rainy7, 0.1)]
wkPoss Cloudy7 = D.possOf [(Cloudy7, 1.0), (Sunny7, 0.7), (Rainy7, 0.7)]
wkPoss Rainy7  = D.possOf [(Rainy7, 1.0), (Cloudy7, 0.6), (Sunny7, 0.4)]

demo_sec7lib :: IO ()
demo_sec7lib = do
  putStrLn "\n-- Possibilistic chain (lib, sup-min):"
  mapM_ (\n -> putStrLn ("  step " ++ show n ++ ": "
         ++ D.showDistList (D.nStepsD n wkPoss Sunny7))) [1, 2, 5]

demo_sec7lib
