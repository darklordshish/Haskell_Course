-- | Раздел 18: обогащённая X и Isbell O -| Spec — из библиотеки (../lib/KanExtension.hs)

data St = StA | StB | StC deriving (Show, Eq, Ord, Enum, Bounded)

homSt :: St -> St -> UnitInterval
homSt x y | x == y = ltop
homSt StA StB = ui 0.7
homSt StB StA = ui 0.7
homSt _   _   = ui 0.5

tauRawSt :: St -> UnitInterval
tauRawSt StA = ui 1.0
tauRawSt StB = ui 0.2   -- нарушение преснопа: hom(A,B)=0.7, tau(A)=1
tauRawSt StC = ui 0.1

demoEnriched :: IO ()
demoEnriched = do
  putStrLn "=== Razdel 18: obogashchyonnaya X i Isbell ==="
  let xs = [StA, StB, StC]
      showQ f = show [ (x, unUI (f x)) | x <- xs ]
  putStrLn $ "  Tranzitivnost hom:  " ++ show (isTransitive homSt xs)
  putStrLn $ "  tauRaw - presnop?   " ++ show (isPresheaf homSt xs tauRawSt)
  let tauHat = yonedaHat homSt xs tauRawSt
  putStrLn $ "  tauHat = " ++ showQ tauHat
  putStrLn $ "  tauHat - presnop?   " ++ show (isPresheaf homSt xs tauHat)
  putStrLn $ "  Edinica Isbell (phi <= Spec(O phi)): "
             ++ show (checkIsbellUnit homSt xs tauHat)
  putStrLn $ "  Treugolnik O Spec O = O: " ++ show (checkIsbellTriangle homSt xs tauHat)
  let fix1 = isbellSpec homSt xs (isbellO homSt xs tauHat)
  putStrLn $ "  Spec(O(tauHat)) = " ++ showQ fix1 ++ " (tight span)"

demoEnriched
