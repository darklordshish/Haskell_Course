-- | Раздел 2+: интервальный билатис — из библиотеки (../lib/Bitopos.hs)

demoBilattice :: IO ()
demoBilattice = do
  putStrLn "=== Razdel 2+: intervalnyj bilatis ==="
  putStrLn $ "  Reshyotka po <=t: " ++ show (checkLatticeLaws leqT joinT meetT)
  putStrLn $ "  Reshyotka po <=k: " ++ show (checkLatticeLaws leqK joinK meetK)
  putStrLn $ "  Interlacing:      " ++ show checkInterlacing
  putStrLn $ "  bot_k = " ++ show bUnknown ++ " (absolyutnoe neznanie)"
  putStrLn $ "  top_k = " ++ show bContra  ++ " (protivorechie, Bel > Pl)"
  putStrLn $ "  joinK neznanie tochn.znanie: " ++ show (joinK bUnknown bTrue)

demoBilattice
