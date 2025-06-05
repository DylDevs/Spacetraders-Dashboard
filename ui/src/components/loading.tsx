import { BarLoader } from "react-spinners"

function Loading({ loading_text, fullscreen }: { loading_text: string, fullscreen: boolean }) {
    if (!fullscreen) {
        return (
            <div className="flex flex-col text-center items-center space-y-5">
                <h2 className="text-xl font-bold">Spacetraders Dashboard</h2>
                <BarLoader color="#ffffff" height={5} loading={true} speedMultiplier={1.2} width={250} />
                <p>{loading_text}</p>
            </div>
        );
    }

    return (
        <div className="flex flex-col w-screen h-screen text-center items-center justify-center space-y-5">
            <h2 className="text-xl font-bold">Spacetraders Dashboard</h2>
            <BarLoader color="#ffffff" height={5} loading={true} speedMultiplier={1.2} width={250} />
            <p>{loading_text}</p>
        </div>
    );
}


export { Loading }