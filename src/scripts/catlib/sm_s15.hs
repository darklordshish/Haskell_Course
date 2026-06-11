-- | Разделы 1-5: субъективная модель — из библиотеки (../lib/SubjectiveModel.hs)

data State = SA | SB | SC deriving (Show, Eq, Ord, Enum, Bounded)

smDemo :: SubjModel State
smDemo = dualConsistent [SA, SB, SC] tau
  where
    tau SA = 1.0
    tau SB = 0.7
    tau SC = 0.3

demoS15 :: IO ()
demoS15 = do
  putStrLn "=== Razdely 1-5: SubjModel iz biblioteki ==="
  putStrLn $ "  Pl{SA,SB}  = " ++ show (smPl smDemo [SA, SB])
  putStrLn $ "  Bel{SA,SB} = " ++ show (smBel smDemo [SA, SB])
  putStrLn $ "  Dualno soglasovana: " ++ show (isDuallyConsistent smDemo)
  -- pl/bel-интегралы (Теорема 1.1)
  let f SA = 0.9
      f SB = 0.5
      f SC = 0.1
  putStrLn $ "  pl-integral f  = " ++ show (plIntegral [SA,SB,SC] (smTau smDemo) f)
  putStrLn $ "  bel-integral f = " ++ show (belIntegral [SA,SB,SC] (smTauBar smDemo) f)
  -- модели знания (п. 1.5)
  let ign = absoluteIgnorance [SA,SB,SC]
      knw = exactKnowledge [SA,SB,SC] SB
  putStrLn $ "  Neznanie:  Pl{SB}=" ++ show (smPl ign [SB]) ++ " Bel{SB}=" ++ show (smBel ign [SB])
  putStrLn $ "  Znanie SB: Pl{SB}=" ++ show (smPl knw [SB]) ++ " Bel{SB}=" ++ show (smBel knw [SB])
  -- образ под phi: X -> Bool
  let img = imageModel smDemo (== SA) [True, False]
  putStrLn $ "  Obraz phi: tau(True)=" ++ show (smTau img True)
             ++ " tau(False)=" ++ show (smTau img False)
  -- Полиморфизм ядра: Pl над Bool = exists, Bel = forall
  putStrLn $ "  [Bool] Pl{2,3}(x>1)  = " ++ show (plMeasure [1,2,3::Int] (> 1) [2,3])
  putStrLn $ "  [Bool] Bel{2,3}(x>1) = " ++ show (belMeasure [1,2,3::Int] (> 1) [2,3])

demoS15
