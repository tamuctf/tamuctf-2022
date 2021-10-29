from pwn import *
import angr
import networkx

p = remote("tamuctf.com", 443, ssl=True, sni="labyrinth")
for binary in range(5):
  with open("elf", "wb") as file:
    file.write(bytes.fromhex(p.recvline().rstrip().decode()))
  proj = angr.Project("elf", load_options={'auto_load_libs': False})
  cfg = proj.analyses.CFG()

  main = cfg.kb.functions.function(name='main').addr

  addrs = list(cfg.kb.functions.keys())
  target = addrs.index(main) + 1
  target = addrs[target]

  log.info(f"finding route to {cfg.kb.functions[target]}")

  def find_viable(path):
    next = proj.factory.call_state(path[0])

    for i in range(1, len(path)):
      simgr = proj.factory.simgr(next)
      simgr.explore(find=path[i])

      next = simgr.found[0]

    return next.posix.dumps(0)

  path = networkx.shortest_path(cfg.kb.callgraph, main, target)
  res = find_viable(path)
  p.sendline(res.hex())

p.interactive()
