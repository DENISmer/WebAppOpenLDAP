import WR_S from "@/components/pages/workroom/workRoom.module.scss"
import {useEffect} from "react";

export const InputItemForEdit = (data: any) => {
    console.log(data.field)
    return (
        <div key={data.key}>
            {data.field && <div className={WR_S.field}>
                {/*if element is empty object (array)*/}
                {typeof data.field === 'object' && data.field.length === 0 &&
                    <div>
                        <input type="text"
                               name={data.key}
                               placeholder={'lenght 0'}
                               value={data.field}
                               onChange={data.handle}
                        />
                            <button>+</button>
                    </div>}

                {/*if element is nah empty object (array)*/}
                {typeof data.field === "object" && data.field.length > 0 &&
                    <div>
                        {data.field.map((item, index) => (
                            <input type="text"
                                   key={index}
                                   name={data.field + index}
                                   value={data.field[index]}
                                   placeholder={'lenght > 0'}
                                   onChange={data.handle}
                            />
                        ))}
                        <p>
                            <button>+</button>
                        </p>
                    </div>
                }

                {/*if element is string */}
                {typeof data.field === "string" && data.field.length > 0 &&
                    <div>
                        <input type="text"
                               placeholder={'string'}
                               value={data.field}
                               onChange={data.handle}
                        />
                    </div>
                }

                {/*if element is number*/}
                {typeof data.field === "number" &&
                    <div>
                        <input type="text"
                               placeholder={'number'}
                               value={data.field}
                               onChange={data.handle}
                        />
                    </div>
                }

                {/*if element is null*/}
                {typeof data.field === null &&
                    <div>
                        <input type="text"
                               placeholder={'null'}
                               value={data.field}
                               onChange={data.handle}
                        />
                    </div>
                }
            </div>}
        </div>
    )
}
