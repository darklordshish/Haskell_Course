-- | Раздел 4+: Gamma = Aut квантали — из библиотеки (../lib/Quantale.hs)

demoGammaAut :: IO ()
demoGammaAut = do
  putStrLn "=== Razdel 4+: Gamma kak avtomorfizmy kvantali ==="
  putStrLn $ "  t^2  - avtomorfizm:  " ++ show (isQuantaleAuto gammaSq)
  putStrLn $ "  sqrt - avtomorfizm:  " ++ show (isQuantaleAuto gammaSqrt)
  putStrLn $ "  theta - avtomorfizm: " ++ show (isQuantaleAuto theta)
             ++ " (eto dualnost, ne avtomorfizm)"
  -- эквивариантность: gamma(Pl_tau E) = Pl_{gamma.tau} E
  let dom = "abc"
      tau c = case c of { 'a' -> 1.0; 'b' -> 0.6; _ -> 0.2 }
      subs = filterM (const [True, False]) dom
      plW t e = unUI (plMeasure dom (ui . t) e)
      equiv gD = all (\e -> ui (gD (plW tau e)) =~ ui (plW (gD . tau) e)) subs
  putStrLn $ "  Ekvivariantnost Pl dlya t^2:  " ++ show (equiv (\t -> t * t))
  putStrLn $ "  Ekvivariantnost Pl dlya sqrt: " ++ show (equiv sqrt)
  let ordInv = and [ (a < b) == (gammaSq a < gammaSq b) | a <- gammaGrid, b <- gammaGrid ]
  putStrLn $ "  Poryadok invarianten: " ++ show ordInv

demoGammaAut
