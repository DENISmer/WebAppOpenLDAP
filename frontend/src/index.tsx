import {render} from "react-dom";
import {CookiesProvider} from "react-cookie";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import React, {lazy, Suspense} from "react";
import GlobalPreloader from "@/components/nav/globalPreloader/globalPreloader";


function App () {

    const WorkRoom = lazy(() => import("@/components/pages/workroom/workRoom"));
    const Login = lazy(() => import("@/components/pages/Login/login"));
    return (<>
        <CookiesProvider defaultSetOptions={{ path: '/' }}>
            {/*<Provider store={store}>*/}
                <BrowserRouter>
                    <Routes>
                        <Route path="/">
                            <Route index element={<Suspense fallback={<GlobalPreloader />}>
                                <WorkRoom />
                            </Suspense>}/>
                            <Route path="login" element={<Suspense fallback={<GlobalPreloader />}>
                                <Login />
                            </Suspense>}/>
                        </Route>
                        <Route path={"*"}
                               element={<Suspense fallback={<GlobalPreloader />}>
                                  <h1>default</h1> {/*<DefaultPage />*/}
                               </Suspense>}
                        />
                    </Routes>
                </BrowserRouter>
            {/*</Provider>*/}
        </CookiesProvider>
    </>)
}
const rootElement = document.getElementById("root");
render(<App/>, rootElement);
