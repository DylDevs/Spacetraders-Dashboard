import { ClipLoader } from "react-spinners"

function Loading({ loading_text }: { loading_text: string }) {
    return (
        <div className="flex flex-col w-screen h-screen text-center items-center justify-center space-y-3">
            <ClipLoader color="#ffffff50" loading={true} size={40} />
            <p className="text-zinc-500">{loading_text}</p>
        </div>
    );
}

export default Loading