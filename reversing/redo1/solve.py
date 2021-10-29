import angr
import claripy

def main():
    proj = angr.Project('./code', load_options={"auto_load_libs": False})
    argv1 = claripy.BVS("argv1", 34 * 8)
    initial_state = proj.factory.entry_state(args=["./code", argv1])

    sm = proj.factory.simulation_manager(initial_state)
    sm.explore(find=lambda s: b"THAT'S THE FLAG!" in s.posix.dumps(1))
    found = sm.found[0]
    return found.solver.eval(argv1, cast_to=bytes)

if __name__ == '__main__':
    print(main())
