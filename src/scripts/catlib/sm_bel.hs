-- | Раздел 14+: Bel = Ran вдоль профунктора дополнения (библиотека: lanAlong/ranAlong)

demoBelKan :: IO ()
demoBelKan = do
  putStrLn "=== Razdel 14+: Bel cherez Ran vdol dopolneniya ==="
  let dom = "abc"
      tau c = case c of { 'a' -> 1.0; 'b' -> 0.6; _ -> 0.2 }
      tauBar = (1 -) . tau
      subs = filterM (const [True, False]) dom
      pl  e = unUI (plMeasure dom (ui . tau) e)
      bel e = unUI (belMeasure dom (ui . tauBar) e)
      chkDual = all (\e -> ui (bel e) =~ theta (ui (pl (filter (`notElem` e) dom)))) subs
  putStrLn $ "  Bel(E) = theta(Pl(X\\E)) na vseh 8 podmnozhestvah: " ++ show chkDual
  putStrLn $ "  theta - dualnyj izomorfizm (max<->min): " ++ show (isDualIso theta)
  mapM_ (\e -> putStrLn $ "    E=" ++ show e ++ "  Pl=" ++ show (pl e)
               ++ "  Bel=" ++ show (bel e)) subs

demoBelKan
