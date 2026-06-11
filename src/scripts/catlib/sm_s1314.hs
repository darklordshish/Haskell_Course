-- | Разделы 13-14: квантале [0,1], топологии Скотта, Lan/Ran — из библиотеки

demoS1314 :: IO ()
demoS1314 = do
  putStrLn "=== Razdely 13-14: quantale, Scott, Kan ==="
  -- законы квантале: одна полиморфная проверка для [0,1] и Bool
  let gridS = [ui 0, ui 0.25, ui 0.5, ui 0.75, ui 1]
  putStrLn $ "  Residuation adj [0,1]: " ++ show (checkResiduationAdj gridS)
  putStrLn $ "  Residuation adj Bool:  " ++ show (checkResiduationAdj [False, True])
  putStrLn $ "  Frame distributivity:  " ++ show (checkFrameDistributivity gridS)
  -- топологии Скотта, индуцированные tau
  let tau c = case c of { 'a' -> 1.0; 'b' -> 0.6; _ -> 0.2 }
  putStrLn $ "  T_up   (t=0.5): " ++ show (scottUpOnX tau 0.5 "abc")
  putStrLn $ "  T_down (t=0.5): " ++ show (scottDownOnX tau 0.5 "abc")
  -- Lan вдоль принадлежности = Pl; Ran вдоль дополнения = Bel
  let dom = "abc"
  putStrLn $ "  Lan{a,b} = Pl  = " ++ show (unUI (plMeasure dom (ui . tau) "ab"))
  putStrLn $ "  Ran{a,b} = Bel = " ++ show (unUI (belMeasure dom (ui . (1 -) . tau) "ab"))

demoS1314
