

-- Связь с библиотекой (../lib/Quantale.hs): t-норма min — это qTensor
-- квантали [0,1], а импликация Гёделя — её residuation qHom.
demo_sec4lib :: IO ()
demo_sec4lib = do
  putStrLn "\n-- Quantale view (lib):"
  putStrLn ("  qTensor 0.7 0.6 = " ++ show (unUI (qTensor (ui 0.7) (ui 0.6))))
  putStrLn ("  qHom 0.8 0.6 (Godel impl) = " ++ show (unUI (qHom (ui 0.8) (ui 0.6))))
  putStrLn ("  residuation law on grid: " ++ show (checkResiduationAdj gammaGrid))

demo_sec4lib
