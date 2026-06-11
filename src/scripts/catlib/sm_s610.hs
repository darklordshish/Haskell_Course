-- | Разделы 6-10: независимость, кондиционирование (residuation), комбинирование

sm1 :: SubjModel Int
sm1 = dualConsistent [1,2,3] (\x -> case x of { 1 -> 1.0; 2 -> 0.5; _ -> 0.3 })

sm2 :: SubjModel Bool
sm2 = dualConsistent [True, False] (\y -> if y then 1.0 else 0.4)

demoS610 :: IO ()
demoS610 = do
  putStrLn "=== Razdely 6-10: nezavisimost i kombinirovanie ==="
  putStrLn $ "  tau12(1,True)  = min(1.0,1.0) = " ++ show (plJointDist sm1 sm2 (1, True))
  putStrLn $ "  tau12(2,False) = min(0.5,0.4) = " ++ show (plJointDist sm1 sm2 (2, False))
  -- условное распределение через residuation (раздел 7+)
  let dom = [(z1, z2) | z1 <- [1,2::Int], z2 <- [1,2::Int]]
      tauJ :: (Int, Int) -> Double
      tauJ (1,1) = 1.0
      tauJ (2,1) = 0.6
      tauJ (1,2) = 0.4
      tauJ (2,2) = 0.4
      tauJ _     = 0.0
  putStrLn $ "  tau(1|2) = " ++ show (condTau dom tauJ 2 1)
  putStrLn $ "  tau(2|1) = " ++ show (condTau dom tauJ 1 2)
  -- комбинирование субъективного и эмпирического (п. 2.2)
  let subj = [1.0, 0.8, 0.5, 0.2]
      empi = [0.9, 0.7, 0.6, 0.3]
  putStrLn $ "  Rangi kombinirovaniya: " ++ show (combineDistributions subj empi 0.5 0.5)

demoS610
