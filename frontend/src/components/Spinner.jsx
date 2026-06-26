export default function Spinner() {
  return (
    <div className="flex w-full items-center justify-center p-24">
      <div className="relative w-24 h-24 border-4 border-swiss-black bg-swiss-white grid grid-cols-2 grid-rows-2">
         {/* Simple Bauhaus/Swiss loading animation */}
         <div className="w-full h-full bg-swiss-red animate-[ping_1.5s_linear_infinite_0s]" />
         <div className="w-full h-full bg-swiss-black animate-[ping_1.5s_linear_infinite_0.3s]" />
         <div className="w-full h-full bg-swiss-black animate-[ping_1.5s_linear_infinite_0.9s]" />
         <div className="w-full h-full bg-swiss-red animate-[ping_1.5s_linear_infinite_0.6s]" />
      </div>
    </div>
  );
}
