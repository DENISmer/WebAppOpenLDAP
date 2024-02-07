import React from "react";
import style from "@/components/main/mainStyle.module.scss"

function Main (){
    return (<>
        <div className={style.main}>
            <div className={style.content}>
                <p>

                    <span>
                        <h5>this is webpack5 config created for development on:</h5>
                <h6>
                    <ul>
                        <li>typescript</li>
                        <li>css, scss</li>
                        <li>scss modules</li>
                        <li>redux</li>
                    </ul>
                </h6>
                    </span>
                </p>

            </div>

        </div>

    </>)
}

export default Main
