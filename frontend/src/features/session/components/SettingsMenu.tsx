import { useEffect, useRef, useState } from "react";

type SettingsMenuProps = {
  onAboutUs?: () => void;
  onLanguage?: () => void;
  onTheme?: () => void;
  onDeleteAll?: () => void;
};

export function SettingsMenu({
  onAboutUs,
  onLanguage,
  onTheme,
  onDeleteAll,
}: SettingsMenuProps) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node)
      ) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="fixed right-5 top-2 size-14 rounded-lg hover:bg-slate-100 p-2"
        aria-label="Settings"
      >
        <img src="src/assets/settings-icon.png" alt="" />
      </button>

      {open && (
        <div className="fixed right-4 top-19 z-50 w-40 overflow-hidden rounded-xl border border-gray-200 bg-zinc-300 shadow-lg">
          <button
            type="button"
            onClick={() => {
              onAboutUs?.();
              setOpen(false);
            }}
            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100"
          >
            About Us
          </button>

          <button
            type="button"
            onClick={() => {
              onLanguage?.();
              setOpen(false);
            }}
            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100"
          >
            Language
          </button>

          <button
            type="button"
            onClick={() => {
              onTheme?.();
              setOpen(false);
            }}
            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100"
          >
            Theme
          </button>

          <button
            type="button"
            onClick={() => {
              onDeleteAll?.();
              setOpen(false);
            }}
            className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
          >
            Delete All
          </button>
        </div>
      )}
    </div>
  );
}